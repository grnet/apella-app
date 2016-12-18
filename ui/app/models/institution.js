import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice} from 'ui/lib/common';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;


export default DS.Model.extend({
  title: DS.attr({formComponent: 'i18n-input-field'}),
  category: DS.attr({
    type: 'select',
    choices: CHOICES.INSTITUTION_CATEGORIES,
    defaultValue: 'Institution'
  }),
  organization: DS.attr(),
  regulatory_framework: DS.attr(),

  title_current: computeI18N('title'),
  category_verbose: computeI18NChoice('category', CHOICES.INSTITUTION_CATEGORIES),
});
