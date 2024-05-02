import re

def k_formatter(k_value):
  if k_value[-1].isdigit():
    return float(k_value.replace('k', '.').replace('K','.')) * 1000
  else:
    return float(k_value.replace('k', '').replace('K','')) * 1000   

def format_value(compact_value):
  try:
    if compact_value is None:
      return None

    if '-' in compact_value:
      splitted = compact_value.replace(' ', '').split('-')
      formatted_values = [k_formatter(value) if ('k' in value or 'K' in value) else float(value) for value in splitted]
      return sum(formatted_values) / len(formatted_values)

    if 'k' in compact_value or 'K' in compact_value:
      return k_formatter(compact_value)

    return float(compact_value)
  except (ValueError, TypeError):
    # Catch ValueError (e.g., invalid conversion to float) or TypeError (e.g., unsupported operation)
    return None

def preprocess_msg(message, setting):
    processedMsg = {}

    entryRegex = r'(?:entry|Entry|ET)\s*[^0-9]*([\d.,k\s-]+)'
    tokenRegex = r'#\w+'
    stlRegex = r'(?:stl|stoploss|STL|Stl|Stoploss|STOPLOSS)\s*[^0-9]*([\d.,kK]+)'
    tpRegex = r'(?:tp|target|TP)\s*[^0-9]*([\d.,kK\s-]+)'


    entryMatch = re.search(entryRegex, message, flags=re.IGNORECASE)
    tokenMatch = re.search(tokenRegex, message, flags=re.IGNORECASE)
    stlMatch = re.search(stlRegex, message, flags=re.IGNORECASE)
    tpMatch = re.search(tpRegex, message, flags=re.IGNORECASE)

    try:
      entryValue = format_value(entryMatch.group(1).replace(',', '.') if entryMatch else None)
    except AttributeError:
      entryValue = None

    try:
      tokenValue = tokenMatch.group(0).replace('#', '').upper() if tokenMatch else None
    except AttributeError:
      tokenValue = None

    try:
      stlValue = format_value(stlMatch.group(1).replace(',', '.') if stlMatch else None)
    except AttributeError:
      stlValue = None

    try:
      tpValue = format_value(tpMatch.group(1).replace(',', '.') if tpMatch else None)
    except AttributeError:
      tpValue = None

    if "long" or "buy" in message.lower():
      action = 'buy'
    elif "short" or "sell" in message.lower():
      action = 'sell'
    else:
      action = None

    if stlValue == None and action == 'buy':
      stlValue = str(entryValue * (1 - setting['stl_pct'])) if entryValue is not None else None
    elif stlValue == None and action == 'sell':
      stlValue = str(entryValue * (1 + setting['stl_pct'])) if entryValue is not None else None
    elif tpValue == None and action == 'buy':
      tpValue = str(entryValue * (1 + setting['tp_pct'])) if entryValue is not None else None
    elif tpValue == None and action == 'sell':
      tpValue = str(entryValue * (1 - setting['tp_pct'])) if entryValue is not None else None

    processedMsg['token'] = tokenValue + 'USDT'
    processedMsg['entry'] = entryValue
    processedMsg['stl'] = stlValue
    processedMsg['tp'] = tpValue
    processedMsg['action'] = action

    return processedMsg
