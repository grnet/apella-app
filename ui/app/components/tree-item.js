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
    handleChange(value, item, model, subModel) {
      let type = model;
      let self = this;
      if (model=='subject-area') { type = 'area' }
      if (subModel) {
        let nodes = get(this, 'nodes');
        nodes.forEach(function(el){
          self.sendAction('onChange', value, el, subModel);
        });
      }
      this.sendAction('onChange', value, item, type);
    }
  }

});
