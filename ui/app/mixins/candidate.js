import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';

const {
  get, computed
} = Ember;
const CHOICES = ENV.APP.resources;

export default Ember.Mixin.create({
  id_passport_file: DS.belongsTo('apella-file'),
  cv: DS.belongsTo('apella-file'),
  diplomas: DS.hasMany('apella-file'),
  publications: DS.hasMany('apella-file'),
  pubs_note: DS.belongsTo('apella-file'),
});

