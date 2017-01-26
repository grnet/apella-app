import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {booleanFormat} from 'ui/lib/common';


export default Ember.Mixin.create({
  department: DS.hasMany('department'),
  manager_role: DS.attr({defaultValue: 'assistant'}),
  can_create_registries: DS.attr({type: 'boolean', defaultValue: false }),
  can_create_positions: DS.attr({type: 'boolean', defaultValue: false }),
  can_create_registries_verbose: booleanFormat('can_create_registries'),
  can_create_positions_verbose: booleanFormat('can_create_positions'),
});
