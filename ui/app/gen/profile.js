import gen from 'ember-gen/lib/gen';

const redirect = {
        routeMixin: {
          beforeModel() {
           this.transitionTo('profile.record.edit', 'me');
          }
        },
      },
      noBreadcrumb = {
        page: {breadcrumb: false}
      },
      { merge } = Ember;


export default gen.CRUDGen.extend({
  modelName: 'profile',
  list: merge(redirect, {menu: {label: 'profile.label', icon: 'pets'}}),
  create: redirect,
  details: redirect,
  edit: merge(noBreadcrumb, {actions: []}),
  record: noBreadcrumb

});
