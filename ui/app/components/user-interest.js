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
  session: Ember.inject.service(),

  subjectAreas: computed('', function() {
    return get(this, 'store').findAll('subject-area');
  }),

  institutions: computed('', function() {
    return get(this, 'store').findAll('institution');
  }),

  userInterests: computed('', function(){
    let user_id = get(this, 'session.session.authenticated.id');
    return get(this, 'store').query('user-interest', {user:user_id });
  }),

  actions: {
    setInterest(value, type){
      alert(type);
    }
  }

});
