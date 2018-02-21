import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './User.css'
import {createForm} from 'rc-form'
import {Input} from '../../components'
import {updateUser} from '../../reducers/user'
import cn from 'classnames'
import Button from 'react-bootstrap/lib/Button'

class User extends React.Component {
  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.updateUser(values)
      }
    })
  }

  render() {
    const {loading, error, user} = this.props
    const {getFieldDecorator, getFieldError} = this.props.form

    return (
      <div className={s.container}>
        <h1 className={s.header}>Account</h1>
        {user && (
          <form className={s.form} onSubmit={this.handleSubmit}>
            {error && (
              <div className={cn('alert alert-danger', s.alert)}>
                {error}
              </div>
            )}
            <div className={s.row}>
              {getFieldDecorator('first_name', {
                initialValue: user.first_name,
              })(
                <Input className='form-control' error={getFieldError('first_name')} label={'First Name'}/>
              )}
            </div>
            <div className={s.row}>
              {getFieldDecorator('last_name', {
                initialValue: user.last_name,
              })(
                <Input className='form-control' error={getFieldError('last_name')} label={'Last Name'}/>
              )}
            </div>
            <div className={s.row}>
              {getFieldDecorator('email', {
                initialValue: user.email,
              })(
                <Input className='form-control' error={getFieldError('email')} label={'Email'}/>
              )}
            </div>
            <Button
              disabled={loading}
              type='submit'
              bsStyle='primary'
              block
            >
              Update
            </Button>
          </form>
        )}
      </div>
    )
  }
}


const mapState = state => ({
  ...state.user,
})

const mapDispatch = {
  updateUser,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(User)))
