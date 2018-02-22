import {combineReducers} from 'redux'
import user from './user'
import global from './global'
import login from './login'
import register from './register'
import home from './home'
import breastCancer from './breastCancer'

export default combineReducers({
  user,
  global,
  login,
  register,
  home,
  breastCancer,
})
