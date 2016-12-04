import Ember from 'ember';
import DS from 'ember-data';

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
  tagName: 'li',

  store: Ember.inject.service(),
  expanded: false,

  toggleIcon: computed('expanded', function(){
    return this.get('expanded')? 'expand-more': 'chevron-right'
  }),

  nodes: computed('', function(){
    let subModel = get(this, 'subModel');
    let query = {};
    query[get(this, 'lookupField')] = get(get(this, 'item'), 'id');
    return this.get('store').query(subModel, query);
  }),

  actions: {
    toggle(item) {
      this.toggleProperty('expanded');
    },
    handleChange(value, item, model) {
      let type = model;
      if (model=='subject-area') { type = 'area' }
      this.sendAction('onChange', value, item, type);
    }
  }

});
