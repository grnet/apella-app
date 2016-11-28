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

  nodes: computed('expanded', function(){
    let self = this;

    set(self, 'loading', true);
    if (get(this, 'expanded')) {
      let item_id = get(get(this, 'item'), 'id');
      let model = get(this, 'model');
      let lookupField = get(this, 'lookupField');
      let field_id = `${lookupField}.id`
      let promise = this.get('store').findAll(model).then(function(items) {
        return Promise.all(items.getEach(lookupField)).then(() => {
          return items.filterBy(field_id, item_id);
        });
      });
      promise.then(function(){
          set(self, 'loading', false);
      });

      return DS.PromiseArray.create({promise});

    }

  }),

  actions: {
    toggle(item) {
      this.toggleProperty('expanded');
    },
    handleChange(value) {
      this.sendAction('foo', value);
    }
  }

});
