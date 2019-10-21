import auditor

from events.registry import chart_view

auditor.subscribe(chart_view.ChartViewCreatedEvent)
auditor.subscribe(chart_view.ChartViewDeletedEvent)
