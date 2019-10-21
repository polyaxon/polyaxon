import activitylogs

from events.registry import chart_view

activitylogs.subscribe(chart_view.ChartViewCreatedEvent)
activitylogs.subscribe(chart_view.ChartViewDeletedEvent)
