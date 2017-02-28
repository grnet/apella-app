import {position} from 'ui/lib/position/fieldsets';

const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;


const pick_edit_fs = function() {
  let role = get(this, 'role'),
    starts_at = get(this, 'model.starts_at'),
    ends_at = get(this, 'model.ends_at'),
    state = get(this, 'model.state'),
    now = moment(),
    before_open = now.isBefore(starts_at),
    open = now.isBetween(starts_at, ends_at, null, []),
    fs = position.edit,
    head = [fs.basic, fs.details],
    res;

  if(state === 'posted') {
    if(before_open) {
      res = head;
    }
    else if (open) {
      res = head.concat(fs.candidacies);
    }
    // closed
    else {
      res = head.concat(fs.candidacies/*, fs.electors_regular, fs.electors_substitite*/);
    }
  }
  else if(state === 'cancelled') {
    res = head;
  }
  // in all other states
  else {
    res = head.concat(fs.candidacies);
  }

  if (state === 'electing') {
    res = head;
  }

  return res;
};

const pick_details_fs_by_state = function(fs, state, before_open, head, display_candidacies) {
  let res;
  if(state === 'posted') {
    if(before_open) {
      res = head;
    }
    else {
      if (display_candidacies) {
        res =  head.concat(fs.candidacies);
      }
      else {
        res = head;
      }
    }
  }
  else if(state === 'cancelled') {
      res =  head/*.concat(fs.history)*/;
  }
  // in all other states
  else {
    if (display_candidacies) {
      res = head.concat(fs.candidacies/*, fs.electors, fs.electors_regular, fs.electors_substitite, fs.committee, fs.election *//*, fs.history, */);
    }
    else {
      res = head;
    }
  }
  return res;
};

const pick_details_fs = function() {
  let role = get(this, 'role'),
    user_id = get(this, 'user.user_id') + '',
    role_id = get(this, 'user.id') + '',
    starts_at = get(this, 'model.starts_at'),
    // ends_at = get(this, 'model.ends_at'),
    state = get(this, 'model.state'),
    now = moment(),
    before_open = now.isBefore(starts_at),
    fs = position.details,
    head = [fs.basic, fs.details],
    position_model = get(this, 'model'),
    store = get(position_model, 'store'),
    /*
     * roles that require extra validations in order to decide if the
     * candidacies fs should be rendered.
     */
    roles_conditional_candidacies = ['candidate', 'professor'],
    committees_members_ids, electors_ids, participations_in_position,
    display_candidacies = false;

  if(roles_conditional_candidacies.indexOf(role) > -1) {
    let candidacies = [];
    store.peekAll('candidacy').forEach(function(candidacy) {
      let candidacy_pos_id = candidacy.belongsTo('position').link().split('/').slice(-2)[0],
        candidate_id = candidacy.belongsTo('candidate').link().split('/').slice(-2)[0];
      if(candidacy_pos_id === position_model.id) {
        candidacies.push(candidate_id);
      }
    });

    if(candidacies.indexOf(user_id) > -1) {
      display_candidacies = true;
    }
    else if (role === 'professor' && !display_candidacies) {
      let user_department_id = get(this, 'user.department').split('/').slice(-2)[0],
        position_department_id = position_model.belongsTo('department').link().split('/').slice(-2)[0];
      if (user_department_id === position_department_id) {
        display_candidacies = true;
      }
      else {
        electors_ids = position_model.hasMany('electors').ids();
        committees_members_ids = position_model.hasMany('committee').ids();
        participations_in_position = electors_ids.concat(committees_members_ids);

        if (participations_in_position.indexOf(role_id) > -1) {
          display_candidacies = true;
        }
      }
    }
  }
  else {
    display_candidacies = true;
  }
 return pick_details_fs_by_state(fs, state, before_open, head, display_candidacies);
};

const pick_create_fs = function() {
  let fs = position.create;
  return [fs.basic].concat(fs.details);
};
export { pick_edit_fs, pick_details_fs, pick_create_fs };
