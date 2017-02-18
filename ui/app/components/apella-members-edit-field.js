import Ember from 'ember';
import TableSelectField from 'ember-gen/components/gen-form-field-select-table/component';

const {
  computed,
  get, set,
  on,
  observer
} = Ember;

export default TableSelectField.extend({
  addMembers: computed('value', function() { return Ember.A([]); }),
  removeMembers: computed('value', function() { return Ember.A([]); }),

  existingMembers: computed.reads('model'),
  removeRowGen: computed('gen.rowGen', function() {
    let component = this;
    return get(this, 'gen.rowGen').extend({
      actions: ['cancel'],
      actionsMap: {
        cancel: {
          label: 'cancel',
          icon: 'undo',
          action: function() { component.send('cancelRemove', ...arguments); },
          permissions: [],
          warn: true,
          confirm: true
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
      let value = get(this, 'value');
      let members = get(this, 'addMembers');

      let removeFromAdd = [];
      items.forEach((item) => {
        if (!value.includes(item)) {
          value.addObject(item);
        } else {
          removeFromAdd.addObject(item);
        }
      });
      removeFromAdd.forEach((item) => {
        members.removeObject(item);
      });
      this.onChange(value);
      set(this, 'showOptions', false);
    }
  }
});
