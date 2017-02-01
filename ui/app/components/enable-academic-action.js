import Ember from 'ember';
import fetch from "ember-network/fetch";
import ENV from 'ui/config/environment';
import Action from 'ember-gen/components/gen-action/component';

const {
  computed,
  get, set,
  computed: { reads }
} = Ember;

export default Action.extend({
  tagName: '',
  context: reads('model'),
  upgrade: false,
  actionParams: {
    raised: true,
    label: 'enable.academic.login.label',
    text: true,
    icon: 'person',
    confirm: true,
    action: function(route, profile, args) {
      let id = profile.get('user_id');
      let url = ENV.APP.shibboleth_login_url + '?login=1&enable-user=' + id;
      if (args && args.upgrade) { url += '&upgrade=1'; }
      window.location = url;
    },
    classNames: 'button-padding',
    prompt: {
      title: 'enable.academic.login',
      message: 'enable.acaedmic.login.confirm.message',
      ok: 'ok',
      cancel: 'cancel'
    }
  }
});
