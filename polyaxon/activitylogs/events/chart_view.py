import activitylogs

from event_manager.events import chart_view

activitylogs.subscribe(chart_view.ChartViewCreatedEvent)
activitylogs.subscribe(chart_view.ChartViewDeletedEvent)
