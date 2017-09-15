import Ember from 'ember';
import moment from 'moment';
import ENV from 'ui/config/environment';
import _ from 'lodash/lodash';

const {
        get
      } = Ember,
      HOLIDAYS = ENV.APP.resource_holidays,
      DATE_FORMAT = ENV.APP.date_format;


export function afterToday(options) {
  return (key, value) => {
    let today = moment().startOf('day');
    value = moment(value).startOf('day');
    if (!value || value.isAfter(today)) {
      return true;
    } else {
      return 'afterToday.message';
    }
  };
}

export function beforeToday(options) {
  return (key, value) => {
    let today = moment().startOf('day');
    value = moment(value).startOf('day');
    if (!value || value.isBefore(today)) {
      return true;
    } else {
      return 'beforeToday.message';
    }
  };
}

export function notHoliday() {
  return (key, value) => {
    // TODO: use moment, startOf is necessary
    var inputDate = new Date(value);
    let day = moment(value).day();
    let formattedDate = moment(value).format('ddd, D/M/YYYY');
    let holiday = _.find(HOLIDAYS, {'date': formattedDate});
    if (holiday){
      return `${holiday['reason_el']} is a holiday. Choose another date`;
    }
    if ([0,6].includes(day)) {
      return `${moment(value).format(DATE_FORMAT)} should not be on weekends`;
    }
    return true;
  };
}

export function afterDays(options) {
  let { on, days } = options;
  /* We include first and last day and we check with function isAfter.
   * So, we need to remove 1 day.
   */
  let count_days = days - 1;
  return (key, value, _o, changes) => {
    let baseDate = moment(get(changes, on)).startOf('days');
    let nextDate = baseDate.add(count_days, 'days');
    if (moment(value).isAfter(nextDate)) {
      return true;
    } else {
      return `ends${days}After.message`;
    }
  };
}

