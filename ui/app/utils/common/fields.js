import {field} from 'ember-gen';

function disable_field(el) {
  return field(el, {
      disabled: true
  })
}

export {disable_field}
