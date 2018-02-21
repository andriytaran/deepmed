import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Login.css'
import {createForm} from 'rc-form'
import {googleLogin, googleLoginFailure, login} from '../../reducers/login'
import {AutofillInput, Row, Col} from '../../components'
import GoogleLogin from 'react-google-login'
import cn from 'classnames'

class Login extends React.Component {
  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.login(values, this.props.redirectUrl)
      }
    })
  }

  render() {
    const {loading, error, googleClientId, googleLogin, googleLoading, googleLoginFailure, redirectUrl} = this.props
    const {getFieldDecorator} = this.props.form

    return (
      <div className={s.container}>
        <h1 className={s.header}>Login</h1>
        <form className={s.form} onSubmit={this.handleSubmit}>
          {error && (
            <div className={cn('alert alert-danger', s.alert)}>
              {error}
            </div>
          )}
          <div className={s.row}>
            {getFieldDecorator('email', {
              initialValue: '',
            })(
              <AutofillInput className='form-control' placeholder='Email'/>
            )}
          </div>
          <div className={s.row}>
            {getFieldDecorator('password', {
              initialValue: '',
            })(
              <AutofillInput className='form-control' type='password' placeholder='Password'/>
            )}
          </div>
          <Row type='flex' gutter={16}>
            <Col xs={24} sm={12} className={s.col}>
              <button
                disabled={loading}
                type="submit"
                className="btn btn-primary btn-block"
              >
                Submit
              </button>
            </Col>
            <Col xs={24} sm={12} className={s.col}>
              <GoogleLogin
                fetchBasicProfile={false}
                clientId={googleClientId}
                scope='email'
                onSuccess={(res) => googleLogin(res, redirectUrl)}
                onFailure={googleLoginFailure}
                style=''
                className={s.googleLoginBtn}
                disabled={googleLoading}
              >
                Sign in with Google
              </GoogleLogin>
            </Col>
          </Row>
        </form>
      </div>
    )
  }
}


const mapState = state => ({
  ...state.login,
  googleClientId: state.global.googleClientId,
})

const mapDispatch = {
  login,
  googleLogin,
  googleLoginFailure,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(Login)))
