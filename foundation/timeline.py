

import datetime
from django.utils import timezone

def date_to_utc(date_obj):
    if date_obj:
        dt = datetime.datetime.combine(date_obj, datetime.time.min)
        dt = timezone.make_aware(dt, datetime.timezone.utc)
        return int(dt.timestamp()) * 1000
    return None

def prepare_timeline_data(country, historical_periods, entities, currencies):
    import logging
    logger = logging.getLogger(__name__)

    timeline_data = []
    categories = []
    current_timestamp = int(timezone.now().timestamp()) * 1000

    # Helper function to add events
    def add_events(items, level, color, label_prefix, model_type):
        for item in items:
            if item.start_date:
                events.append({
                    'name': f"{label_prefix}: {item.name}",
                    'unique_id': item.id,
                    'model_type': model_type,
                    'start': date_to_utc(item.start_date),
                    'end': date_to_utc(item.end_date) if item.end_date else current_timestamp,
                    'level': level,
                    'color': color
                })
            else:
                logger.warning(f"Skipping {label_prefix} '{item.name}' because it lacks a valid start date.")

    # Collect all events with their start_date and end_date
    events = []

    # Add Country event if it has both start and end dates
    if country.start_date:
        events.append({
            'name': f"Country: {country.name}",
            'unique_id': country.id,
            'model_type': 'country',
            'start': date_to_utc(country.start_date),
            'end': date_to_utc(country.end_date) if country.end_date else current_timestamp,
            'level': 0,
            'color': '#4CAF50'
        })

    # Add Historical Periods, Entities, and Currencies
    add_events(historical_periods, 1, '#2196F3', 'Historical Period', 'historicalperiod')
    add_events(entities, 2, '#FFC107', 'Entity', 'entity')
    add_events(currencies, 3, '#E91E63', 'Currency', 'currency')

    if not events:
        return [], []

    # Sort events by start date and assign unique y index
    events.sort(key=lambda x: x['start'])
    categories = [event['name'] for event in events]
    category_indices = {category: index for index, category in enumerate(categories)}

    # Assign y index to events
    for event in events:
        event['y'] = category_indices[event['name']]

    return events, categories