import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice} from 'ui/lib/common';

const CHOICES = ENV.APP.resources;


export default DS.Model.extend({
  title: DS.attr({formComponent: 'i18n-input-field'}),
  category: DS.attr({
    type: 'select',
    choices: CHOICES.INSTITUTION_CATEGORIES,
    defaultValue: 'Institution',
    translate: true,
  }),
  organization: DS.attr({displayComponent: 'url-display'}),
  regulatory_framework: DS.attr({displayComponent: 'url-display'}),

  title_current: computeI18N('title'),
  category_verbose: computeI18NChoice('category', CHOICES.INSTITUTION_CATEGORIES),
});
