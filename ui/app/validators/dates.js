import Ember from 'ember';
import buildMessage from 'ember-changeset-validations/utils/validation-errors';
import moment from 'moment';
import ENV from 'ui/config/environment';
import _ from 'lodash/lodash';

const {
        get
      } = Ember,
      TODAY = new Date(),
      HOLIDAYS = ENV.APP.resource_holidays,
      DATE_FORMAT = ENV.APP.date_format;


export function afterToday(options) {
  return (key, value) => {
    if (moment(value).isAfter(TODAY)) {
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
