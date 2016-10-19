import Ember from 'ember';

export default Ember.Mixin.create({
  title_current: Ember.computed('title', 'i18n.locale',  function() {
    let lang = this.get('i18n.locale');
    return this.get('title')[lang];
  }),

});
