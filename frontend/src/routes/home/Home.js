import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Home.css'
import {Row, Col, Link} from '../../components'
import {BC_FORM_ROUTE} from '../../routes'
import cn from 'classnames'

class Home extends React.Component {
  render() {
    return (
      <div className={s.container}>
        <Row type='flex' justify='center' gutter={16}>
          <Col>
            <h2 className={s.header}>DeepMed Oncology</h2>
            <Row type='flex' justify='center' align='middle' gutter={16} className={s.modules}>
              <Col>
                <Link to={BC_FORM_ROUTE}>
                  <div className={s.module}>
                    Breast Cancer
                  </div>
                </Link>
              </Col>
              <Col>
                <span>
                  <div className={cn(s.module, s.disabled)}>
                    Prostate Cancer
                    <br/>
                    <span className={s.muted}>(Coming soon)</span>
                  </div>
                </span>
              </Col>
              <Col>
                <span>
                  <div className={cn(s.module, s.disabled)}>
                    Colon cancer
                    <br/>
                    <span className={s.muted}>(Coming soon)</span>
                  </div>
                </span>
              </Col>
              <Col>
                <span>
                  <div className={cn(s.module, s.disabled)}>
                    Lung cancer
                    <br/>
                    <span className={s.muted}>(Coming soon)</span>
                  </div>
                </span>
              </Col>
            </Row>
          </Col>
          <Col>
            <h2 className={s.header}>DeepMed Pediatrics</h2>
            <Row type='flex' justify='center' align='middle' gutter={16} className={s.modules}>
              <Col>
                <span>
                  <div className={cn(s.module, s.disabled)}>
                    Head Trauma
                    <br/>
                    <span className={s.muted}>(Coming soon)</span>
                  </div>
                </span>
              </Col>
              <Col>
                <span>
                  <div className={cn(s.module, s.disabled)}>
                    Sepsis
                    <br/>
                    <span className={s.muted}>(Coming soon)</span>
                  </div>
                </span>
              </Col>
            </Row>
          </Col>
        </Row>
      </div>
    )
  }
}

const mapState = state => ({
})

const mapDispatch = {
}

export default connect(mapState, mapDispatch)(withStyles(s)(Home))
