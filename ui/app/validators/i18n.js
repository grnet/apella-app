import Ember from 'ember';

export function i18nValidate(validators) {
  return (key, newValue, oldValue, changes) => {
    // errors_lang is an object with languages as keys.
    // It will be used by the component to extract errors for each language
    var errors_lang = {};
    var result = true;

    Object.keys(newValue).forEach(function(lang){
      let newVal = newValue[lang];
      // oldValue might be not set yet (for example when creating a new model)
      let oldVal = '';
      if (oldValue && oldValue.hasOwnProperty(lang)) {
        oldVal = oldValue[lang];
      }
      // if there are any, errors are expected to be an array of strings
      let errors = [];

      validators.forEach(function(validator){
        // a will be true or a string with an error message
        let a = validator(key, newVal, oldVal);
        // If a is a string, populate errors_lang with this error message.
        if (a !== true) {
          errors.push(a);
          errors_lang[lang] = errors;
          result = a;
        }
      });
    });

    // If there are indeed some  errors, we return errors_lang
    if (result !== true) {
      return errors_lang;
    }
    return result;
  };
}

