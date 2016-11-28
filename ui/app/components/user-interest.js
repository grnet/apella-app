import Ember from 'ember';
import _ from 'lodash/lodash';

const {
  RSVP: { Promise },
  assert,
  get,
  set,
  isArray,
  computed,
  computed: { alias, equal, gt, map }
} = Ember;

export default Ember.Component.extend({
  classNames: 'interest',
  store: Ember.inject.service(),

  subjectAreas: computed('', function() {
    return this.get('store').findAll('subject-area');
  }),

  institutions: computed('', function() {
    return this.get('store').findAll('institution');
  }),

  actions: {
    foo(value){
      debugger;
      alert(value);
    }
  }

});
