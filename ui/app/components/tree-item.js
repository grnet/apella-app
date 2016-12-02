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
  loading: false,

  toggleIcon: computed('expanded', function(){
    return this.get('expanded')? 'expand-more': 'chevron-right'
  }),

  nodes: computed('', function(){
    let self = this;
    set(self, 'loading', true);
    let item_id = get(get(this, 'item'), 'id');
    let subModel = get(this, 'subModel');
    let lookupField = get(this, 'lookupField');
    let field_id = `${lookupField}.id`
    let promise = this.get('store').findAll(subModel).then(function(items) {
      return Promise.all(items.getEach(lookupField)).then(() => {
        return items.filterBy(field_id, item_id);
      });
    });
    promise.then(function(){
        set(self, 'loading', false);
    });
    return DS.PromiseArray.create({promise});
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
