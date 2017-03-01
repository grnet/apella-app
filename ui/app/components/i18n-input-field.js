import Ember from 'ember';

const {
  set,
  computed
} = Ember;


export default Ember.Component.extend({

  i18n: Ember.inject.service(),

  locales: computed('i18n.locale', 'i18n.locales', function() {
    const i18n = this.get('i18n');
    return this.get('i18n.locales').map(function (loc) {
      return { id: loc, text: i18n.t('language-select.language.' + loc) };
    });
  }),

  errorsI18N: computed('errors.[]', function(){
    let errors = this.get('errors');

    if (errors.length > 0) {
      // client side errors, list of strings
      if (typeof errors[0] === 'string') {
        let _errors = {};
        this.get('i18n.locales').forEach((loc) => {
          _errors[loc] = errors;
        });
        return _errors;
      }
      // server side errors, object with locale specific errors
      return errors[0];
    }
    return [];
  }),

  actions: {

    handleChange(lang, newVal){
      let value = this.get('value');
      // If value is undefined (for example when creating a new model), we
      // must create an empty value object with key->lang and value->newVal
      // If not, we just set the newVal
      if (!value) {
        value = {};
        value[lang] = newVal;
      } else {
        set(value, lang, newVal);
      }

      this.onChange(value);
    },

  }
});
