import Ember from 'ember';
import TableSelectField from 'ember-gen/components/gen-form-field-select-table/component';

const {
  computed,
  get, set,
  on,
  observer
} = Ember;

export default TableSelectField.extend({
  activeSubTable: 'add',
  addMembers: computed('value', function() { return Ember.A([]); }),
  removeMembers: computed('value', function() { return Ember.A([]); }),

  // two snapshots of value array, one to keep reference to the initially selected items
  allMembers: computed('value.[]', function() { return Ember.A(get(this, 'value').concat()); }),
  valueMembers: computed('value', function() { return Ember.A(get(this, 'value').concat()); }),

  existingMembers: computed.reads('model'),
  removeRowGen: computed('gen.rowGen', function() {
    let component = this;
    return get(this, 'gen.rowGen').extend({
      actions: ['cancel'],
      actionsMap: {
        cancel: {
          label: 'restore',
          icon: 'undo',
          action: function() { component.send('cancelRemove', ...arguments); },
          permissions: [],
          warn: true,
          confirm: true,
        }
      }
    });
  }),

  actions: {

    cancelRemove(item, model) {
      let removeMembers = get(this, 'removeMembers');
      let value = get(this, 'value') || [];
      value.addObject(model);
      removeMembers.removeObject(model);
    },

    handleItemRemove(item, model) {
      let addMembers = get(this, 'addMembers');
      let removeMembers = get(this, 'removeMembers');
      let value = get(this, 'value') || [];

      if (addMembers.includes(model)) {
        addMembers.removeObject(model);
        value.removeObject(model);
        return false;
      }
      if (value.includes(model)) {
        removeMembers.addObject(model);
        value.removeObject(model);
        this.onChange(value);
      }
      return false;
    },

    handleAddItems(items) {

      let valueMembers = get(this, 'valueMembers');
      let value = get(this, 'value');
      let toAdd = get(this, 'addMembers');
      let toRemove = get(this, 'removeMembers');

      // remove deselected items
      let _remove = [];
      toAdd.forEach((item) => {
        if (!items.includes(item)) {
          _remove.push(item);
        }
      });
      _remove.forEach((item) => { toAdd.removeObject(item); });

      // remove previously existing
      valueMembers.forEach((item) => {
        if (!items.includes(item)) {
          toRemove.addObject(item);
        }
      });

      // remove from toRemove
      _remove = [];
      toRemove.forEach((item) => {
        if (items.includes(item)) {
          _remove.push(item); 
        }
      });
      _remove.forEach((item) => { toRemove.removeObject(item); });

      // add newly selected items
      items.forEach((item) => {
        if (!valueMembers.includes(item)) {
          if (!toAdd.includes(item)) {
            toAdd.addObject(item);
          }
        }
      });

      value.setObjects(items);
      this.onChange(value);
      set(this, 'showOptions', false);
    },

    hideOptions: function() {
      set(this, 'showOptions', false);
      set(this, 'allMembers', get(this, 'value'));
    }
  }
});
