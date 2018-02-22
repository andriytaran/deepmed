import React from 'react'
import BcForm from './BcForm'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'DeepMed',
    component: <AppLayout><BcForm/></AppLayout>,
  }
}

export default action
