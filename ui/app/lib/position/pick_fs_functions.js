import {position} from 'ui/lib/position/fieldsets';
import _ from 'lodash/lodash';

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
    position_type = get(this, 'model.position_type'),
    open = now.isBetween(starts_at, ends_at, null, []),
    fs = position.edit,
    res;

  let head = [fs.basic, fs.details, fs.assistant_files];

  if(state === 'posted') {
    if(before_open) {
      res = head;
    }
    else if (open) {
      res = head.concat(fs.candidacies);
    }
    // closed
    else {
      res = head.concat(fs.candidacies);
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
    res = res.concat(fs.electors, fs.electors_regular, fs.electors_substitite, fs.committee, fs.election);
  }

  return res;
};

const pick_details_fs_by_state = function(fs, state, before_open, display_candidacies, limited_permissions) {
  let res,
    head = [fs.basic, fs.details, fs.assistant_files],
    tail = [fs.contact, fs.history];

  if(limited_permissions) {
    return res = [fs.basic, fs.details, fs.contact];
  }
  else if(state === 'posted') {
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
    res =  head;
  }
  // in all other states
  else {
    if (display_candidacies) {
      res = head.concat(fs.candidacies, fs.electors, fs.electors_regular, fs.electors_substitite, fs.committee, fs.election);
    }
    else {
      res = head.concat(fs.electors, fs.electors_regular, fs.electors_substitite, fs.committee, fs.election);
    }
  }
  return res.concat(tail);
};

const pick_details_fs = function() {
  let role = get(this, 'role'),
    user_id = get(this, 'user.user_id'),
    role_id = get(this, 'user.id'),
    starts_at = get(this, 'model.starts_at'),
    // ends_at = get(this, 'model.ends_at'),
    state = get(this, 'model.state'),
    now = moment(),
    before_open = now.isBefore(starts_at),
    fs = position.details,
    position_type = get(this, 'model.position_type'),
    position_code = get(this, 'model.code').replace('APP', ''),
    position_model = get(this, 'model'),
    store = get(position_model, 'store'),
    /*
     * roles that require extra validations in order to decide if the
     * candidacies fs should be rendered.
     */
    roles_conditional_candidacies = ['candidate', 'professor'],
    committees_members_ids, electors_ids, participations_in_position,
    display_candidacies = false,
    limited_permissions = false;


  if(roles_conditional_candidacies.indexOf(role) > -1) {
    let candidacies = [];
    let candidates_ids = [];

    /*
     * Check if the user is a candidate for this position.
     * On getModel we fetch the candidacies, so here we use the peekAll function
     * to check them and keep only the data we need for each candidacy.
     * The latest candidacies for the position are normally fetched but if the
     * user has already visited the candidacies list view, all the candidacies
     * are stored in Ember's local storage.
     * We keep only the candidacies that belong to the position for which we
     * display the details.
     * In order to keep these candidacies we check if the position they belong
     * is equal to the most recent instance of this position, as extracted from
     * the position code.
     */

    candidacies = store.peekAll('candidacy').map(function(candidacy) {
      let candidacy_pos_id = candidacy.belongsTo('position').link().split('/').slice(-2)[0];
      if (candidacy_pos_id == position_code) {
        return {
          candidate_id: candidacy.belongsTo('candidate').link().split('/').slice(-2)[0],
          candidacy_is_posted: (get(candidacy, 'state') === 'posted'),
          updated_at_ms: Date.parse(get(candidacy, 'updated_at')),
          updated_at: get(candidacy, 'updated_at')
        };
      }
    });

    /*
     * Only the latest candidacies for the position are kept.
     * The candidacies are sorted by descending updated_at date and then only the
     * first occurrence for each candidate is kept.
    */

    candidacies.sort(function (a, b) {
        return b.updated_at_ms - a.updated_at_ms;
    });

    candidacies = _.uniq(candidacies, 'candidate_id');
    // remove undefined values from candidacies
    candidacies = _.compact(candidacies);

    // If there are no candidacies, candidacy.candidate_id and
    // candidacy.candidacy_is_posted produce typeError
    if (candidacies.length >0 ) {
      candidacies.forEach(function(candidacy) {
        let candidate_id = candidacy.candidate_id,
          candidacy_is_posted = candidacy.candidacy_is_posted;

        /*
         * if the candidacy is posted and not cancelled keep the id of the
         * candidate.
         */
        if(candidacy_is_posted) {
          candidates_ids.push(candidate_id);
        }
        // if the candidacy is cancelled limit the view permissions of the user.
        else if(user_id === candidate_id) {
          limited_permissions = true;
        }
      });
    }
    // Show candidacies fieldset only in fellow candidates
    if(candidates_ids.indexOf(user_id) > -1) {
      display_candidacies = true;
    }
    // If the user is not an *active* candidate and he is a professor
    else if (role === 'professor') {
      let user_department = get(this, 'user.department') || "",
        user_department_id = user_department.split('/').slice(-2)[0],
        position_department_id = position_model.belongsTo('department').link().split('/').slice(-2)[0];
      /*
       * If the professor belongs to the department of the position should be
       * able to see candidacies and their details.
       */
      if (user_department_id === position_department_id) {
        display_candidacies = true;
        /*
         * If the user is a professor of the department of the position and an
         * ex candidate, should see what the other professors see not what other
         * ex candidates see.
         */
        limited_permissions = false;
      }
      /*
       * If the professor doesn't belong to the department of the position
       * should check if he/she is a elector or a member of the committee
       * (regular or substitute).
       */
      else {
        electors_ids = position_model.hasMany('electors').ids();
        committees_members_ids = position_model.hasMany('committee').ids();
        participations_in_position = electors_ids.concat(committees_members_ids);

        if (participations_in_position.indexOf(role_id) > -1) {
          display_candidacies = true;
          limited_permissions = false;
        }
      }
    }
  }
  /*
   * If the user is assistant, institutionmanager, helpdeskadmin, helpdeskuser
   * and ia able to see the details of the position, can also see the
   * candidacies.
   */
  else {
    display_candidacies = true;
  }
  return pick_details_fs_by_state(fs, state, before_open, display_candidacies, limited_permissions);
};

const pick_create_fs = function() {
  let fs = position.create;
  return [fs.basic].concat(fs.details);
};
export { pick_edit_fs, pick_details_fs, pick_create_fs };
