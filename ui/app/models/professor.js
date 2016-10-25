import DS from 'ember-data';
import ENV from 'ui/config/environment';
import User from 'ui/models/user';
import {normalizeUser, serializeUser} from 'ui/utils/common/users';

const CHOICES = ENV.APP.resource_choices;

export default User.extend({
  __api__: {
    normalize: normalizeUser,
    serialize: serializeUser
  },
  institution: DS.belongsTo('institution', {attrs: {optionLabelAttr: 'title_current'}}),
  rank: DS.attr({type: 'select', choices: CHOICES.RANKS, defaultValue:'Assistant Professor'}),
  is_foreign: DS.attr({type: 'boolean', defaultValue: false }),
  speaks_greek: DS.attr({type: 'boolean', defaultValue: true }),
  cv_url: DS.attr(),
  fek: DS.attr(),
  fek_discipline: DS.attr(),
  discipline_free_text: DS.attr()

});
