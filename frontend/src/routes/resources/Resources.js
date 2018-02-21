import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Resources.css'
import {Col, Row, Spin} from '../../components'
import isEmpty from 'lodash/isEmpty'

class Resources extends React.Component {
  render() {
    const {resources} = this.props
    return (
      <div className={s.container}>
        {!isEmpty(resources) ? (
          <React.Fragment>
            <Row type='flex' gutter={16}>
              <Col xs={24} md={12} className={s.col}>
                <div className={s.card}>
                  <h2 className={s.cardHeader}>
                    Google Links <span className={s.info}>({resources.google_links.length})</span>
                  </h2>
                  <div className={s.cardContent}>
                    {resources.google_links.map((item, i) =>
                      <div key={i} className={s.link}>
                        <a rel='nofollow' href={item.link}>{item.title}</a>
                        <p>{item.description}</p>
                      </div>
                    )}
                  </div>
                </div>
              </Col>
              <Col xs={24} md={12} className={s.col}>
                <div className={s.card}>
                  <h2 className={s.cardHeader}>
                    Links to Pubmed Studies <span className={s.info}>({resources.pubmed.length})</span>
                  </h2>
                  <div className={s.cardContent}>
                    {resources.pubmed.map((item, i) =>
                      <div key={i} className={s.link}>
                        <a rel='nofollow' href={item.link}>{item.title}</a>
                        <p>{item.description}</p>
                      </div>
                    )}
                  </div>
                </div>
              </Col>
            </Row>
            <Row type='flex' gutter={16}>
              <Col xs={24} md={12} className={s.col}>
                <div className={s.card}>
                  <h2 className={s.cardHeader}>
                    Blogs and Posts RegardingSimilar Cancer Diagnosis <span
                    className={s.info}>({resources.blogs_and_posts.length})</span>
                  </h2>
                  <div className={s.cardContent}>
                    {resources.blogs_and_posts.map((item, i) =>
                      <div key={i} className={s.link}>
                        <a rel='nofollow' href={item.link}>{item.title}</a>
                        <p>{item.description}</p>
                      </div>
                    )}
                  </div>
                </div>
              </Col>
              <Col xs={24} md={12} className={s.col}>
                <div className={s.card}>
                  <h2 className={s.cardHeader}>
                    Most Recent News Articles <span className={s.info}>({resources.news_articles.length})</span>
                  </h2>
                  <div className={s.cardContent}>
                    {resources.news_articles.map((item, i) =>
                      <div key={i} className={s.link}>
                        <a rel='nofollow' href={item.link}>{item.title}</a>
                        <p>{item.description}</p>
                      </div>
                    )}
                  </div>
                </div>
              </Col>
            </Row>
          </React.Fragment>
        ) : (
          <Spin spinning/>
        )}
      </div>
    )
  }
}

const mapState = state => ({
  ...state.diagnosis,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(Resources))
