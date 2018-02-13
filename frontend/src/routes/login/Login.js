import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Login.scss'
import {createForm} from 'rc-form'
import {login} from '../../reducers/login'

class Login extends React.Component {
  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.login(values)
      }
    })
  }

  render() {
    const {loading, error} = this.props
    const {getFieldDecorator} = this.props.form

    return (
      <div className="container login">
        <h1 className="text-center">Login</h1>
        <div className="login-container margin-top-medium">
          <form onSubmit={this.handleSubmit}>
            {error && (
              <div className="row">
                <div className="col-sm-12">
                  <div className='alert alert-danger'>
                    {error}
                  </div>
                </div>
              </div>
            )}
            <div className="form-group">
              {getFieldDecorator('email', {
                initialValue: '',
              })(
                <input className='form-control' placeholder='Email'/>
              )}
            </div>
            <div className="form-group">
              {getFieldDecorator('password', {
                initialValue: '',
              })(
                <input className='form-control' type='password' placeholder='Password'/>
              )}
            </div>
            <button
              disabled={loading}
              type="submit"
              className="btn btn-primary btn-block"
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    )
  }
}


const mapState = state => ({
  ...state.login,
})

const mapDispatch = {
  login,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(Login)))
