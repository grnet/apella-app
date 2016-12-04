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

  userInterests: computed('model', function(){
    return this.get('model');
  }),


  actions: {
    setInterest(value, item, type){
      if (value) {
        this.get('userInterests').get(type).removeObject(item);
      } else {
        this.get('userInterests').get(type).pushObject(item);
      }
    },
    saveInterest() {
      let user  = get(this, 'store').peekRecord('profile', 'me');
      let model = get(this, 'model');
      user.then((u) => {
        model.set('user', u);
        model.save();
      })
    }
  }

});
