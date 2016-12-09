import Ember from 'ember';
import _ from 'lodash/lodash';

const {
  RSVP: { Promise, all },
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


  user: computed('', function(){
    return get(this, 'store').findRecord('profile', 'me');
  }),

  subjectAreas: computed('', function() {
    return get(this, 'store').query('subject-area', {ordering:'id'});
  }),

  institutions: computed('', function() {
    return get(this, 'store').query('institution', {ordering:'id'});
  }),

  partialArea: computed('userInterests.subject.[]', function() {
    let ui = get(this, 'userInterests').get('subject');
    let promise = ui.then((items) => {
      return Ember.RSVP.all(items.getEach('area'));
    });
    return DS.PromiseArray.create({promise});
   }),

  partialInstitution: computed('userInterests.department.[]', function() {
    let ui = get(this, 'userInterests').get('department');
    let promise = ui.then((items) => {
      return Ember.RSVP.all(items.getEach('institution'));
    });
    return DS.PromiseArray.create({promise});
   }),

  userInterests: computed('model', 'user',  function(){
    let user = get(this, 'user')
    if (this.get('model') ) {
      return this.get('model');
    } else {
      return this.get('store').createRecord('user-interest', {
        user: user
      });

    }
  }),

  successMessage: null,
  errorMessage: null,
  setSuccessMessage: function() {
    set(this, 'successMessage', 'form.saved');
  },
  setErrorMessage: function(msg) {
    set(this, 'errorMessage', msg);
  },

  resetMessages: function() {
    set(this, 'successMessage', null);
    set(this, 'errorMessage', null);
  },


  actions: {
    setInterest(value, item, type){
      if (value) {
        this.get('userInterests').get(type).removeObject(item);
      } else {
        this.get('userInterests').get(type).pushObject(item);
      }
    },
    saveInterest() {
      this.resetMessages();
      let user  = get(this, 'user');
      let model = get(this, 'userInterests');
      user.then((u) => {
        model.set('user', u);
        model.save().then((model) => {
          this.setSuccessMessage();
        }).catch((err) => {
          this.setErrorMessage(err)
        });
      })
    }
  }

});
