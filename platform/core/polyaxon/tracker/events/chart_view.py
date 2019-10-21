import tracker

from events.registry import chart_view

tracker.subscribe(chart_view.ChartViewCreatedEvent)
tracker.subscribe(chart_view.ChartViewDeletedEvent)
