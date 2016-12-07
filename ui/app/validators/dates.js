import Ember from 'ember';
import buildMessage from 'ember-changeset-validations/utils/validation-errors';
import moment from 'moment';
import ENV from 'ui/config/environment';
import _ from 'lodash/lodash';

const {
        get
      } = Ember,
      TODAY = new Date(),
      TOMORROW = moment(TODAY).add(1, 'day'),
      HOLIDAYS = ENV.APP.resource_holidays,
      DATE_FORMAT = ENV.APP.date_format;


export function afterToday(options) {
  return (key, value) => {
    if (moment(value).isAfter(TOMORROW)) {
      return true;
    } else {
      return `${moment(value).format(DATE_FORMAT)} should be after today`;
    }
  };
}

export function beforeToday(options) {
  return (key, value) => {
    if (moment(value).isBefore(TODAY)) {
      return true;
    } else {
      return `${moment(value).format(DATE_FORMAT)}  should be before today`;
    }
  };
}

export function notHoliday() {
  return (key, value) => {
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

  return (key, value, _o, changes) => {
    let baseDate = get(changes, 'starts_at');
    let nextDate = moment(baseDate).add(days, 'days');
    if (moment(value).isAfter(nextDate)) {
      return true;
    } else {
      return `End date should be ${days} days after start date`;
    }
  };
}

