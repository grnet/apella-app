import DS from 'ember-data';
import ENV from 'ui/config/environment';
import titleI18NMixin from 'ui/mixins/title-current';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      INSTITUTION_CATEGORIES = ENV.APP.resources.INSTITUTION_CATEGORIES;


export default DS.Model.extend(titleI18NMixin, {
  title: DS.attr({formComponent: 'i18n-input-field'}),
  category: DS.attr({
    type: 'select',
    choices: INSTITUTION_CATEGORIES,
    defaultValue: 'Institution'
  }),
  organization: DS.attr(),
  regulatory_framework: DS.attr(),

  category_verbose: computed('category', 'i18n.locale', function(){
    let el = this.get('category');
    let list = INSTITUTION_CATEGORIES;
    return  this.get('i18n').t(get_label(list, el));
  }),

});
