import auditor

from event_manager.events import chart_view

auditor.subscribe(chart_view.ChartViewCreatedEvent)
auditor.subscribe(chart_view.ChartViewDeletedEvent)
