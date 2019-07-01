import * as moment from 'moment';

export const humanizeMetric = (value: number) => {
  if (Math.abs(value) < 10) {
    return Math.round(value * 1000) / 1000;
  } else if (Math.abs(value) < 100) {
    return Math.round(value * 100) / 100;
  } else {
    return Math.round(value * 10) / 10;
  }
};

export const humanizeTimeDelta = (startDate: string | Date, endtDate: string | Date): string | null => {
  if (startDate == null || endtDate == null) {
    return null;
  }

  let seconds = moment(endtDate).diff(moment(startDate), 'seconds');
  let minutes = moment(endtDate).diff(moment(startDate), 'minutes');
  let hours = moment(endtDate).diff(moment(startDate), 'hours');
  const days = moment(endtDate).diff(moment(startDate), 'days');

  hours = hours % 24;
  minutes = minutes % 60;
  seconds = seconds % 60;
  let result = '';

  if (days >= 1) {
    result += `${days}d`;
    if (hours >= 1) {
      result += ` ${hours}h`;
    }
    if (minutes >= 1) {
      result += ` ${minutes}m`;
    }
    return result;
  }

  if (hours >= 1) {
    result += `${hours}h`;
    if (hours >= 1) {
      result += ` ${minutes}m`;
    }
    return result;
  }

  if (minutes >= 1) {
    result = `${minutes}m`;
    if (seconds >= 1) {
      result += ` ${seconds}s`;
    }
    return result;
  }

  return `${seconds}s`;
};
