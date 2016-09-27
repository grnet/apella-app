import DS from 'ember-data';


export default DS.Model.extend({
  username: DS.attr({label: 'manager.label.username'}),
  last_name: DS.attr({label: 'manager.label.last_name'}),
  last_name_latin: DS.attr({label: 'manager.label.last_name_latin'}),
  first_name: DS.attr({label: 'manager.label.first_name'}),
  first_name_latin: DS.attr({label: 'manager.label.first_name_latin'}),
  fathers_name: DS.attr({label: 'manager.label.fathers_name'}),
  fathers_name_latin: DS.attr({label: 'manager.label.fathers_name_latin'}),
  id_num: DS.attr({label: 'manager.label.id_num'}),
  psw: DS.attr({label: 'manager.label.psw'}),
  confirm_psw: DS.attr({label: 'manager.label.confirm_psw'}),
  email: DS.attr({label: 'manager.label.email'}),
  mobile: DS.attr({label: 'manager.label.mobile'}),
  phone: DS.attr({label: 'manager.label.phone'})
});
