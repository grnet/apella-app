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
    let subModelType = get(this, 'subModelType');
    let query = {};
    query[get(this, 'lookupField')] = get(get(this, 'item'), 'id');
    return this.get('store').query(subModelType, query);

  }),

  actions: {
    toggle(item) {
      this.toggleProperty('expanded');
    },
    handleChange(value, item, modelType, subModelType) {
      let type = modelType;
      let self = this;
      if (modelType=='subject-area') { type = 'area' }
      if (subModelType) {
        let nodes = get(this, 'nodes');
        nodes.forEach(function(el){
          self.sendAction('onChange', value, el, subModelType);
        });
      }
      this.sendAction('onChange', value, item, type);
    }
  }

});
