import tracker

from event_manager.events import chart_view

tracker.subscribe(chart_view.ChartViewCreatedEvent)
tracker.subscribe(chart_view.ChartViewDeletedEvent)
