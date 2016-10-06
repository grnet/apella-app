import Ember from 'ember';
import buildMessage from 'ember-changeset-validations/utils/validation-errors';
import moment from 'moment';

export function afterToday(options) {
  return (key, value) => {
    var today = new Date();
    var inputDate = new Date(value);
    if (inputDate.getTime() >=today.getTime()) {
      return true;
    } else {
      let msg = moment(value).format('DD/MM/YYYY') + ' should be after today';
      console.log(msg);
      return msg;
    }
  };
}

export function beforeToday(options) {
  return (key, value) => {
    var today = new Date();
    var inputDate = new Date(value);
    if (inputDate.getTime() <today.getTime()) {
      return true;
    } else {
      let msg = moment(value).format('DD/MM/YYYY') + ' should be before today';
      console.log(msg);
      return msg;
    }
  };
}
