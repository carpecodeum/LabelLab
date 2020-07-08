import React, { Component } from 'react'
import update from 'immutability-helper'
import { genId, colors } from './utils'

export function withHistory(Comp) {
  return class HistoryLayer extends Component {
    constructor(props) {
      super(props)
      const { labeldata, labels } = props
      let figures = {}

      labels.map(label => {
        console.log('label map lablel app his hoc')
        return (figures[label.id] = [])})
      figures.__temp = []
      Object.keys(labeldata).forEach(key => {
        figures[key] = (figures[key] || []).concat(labeldata[key])
      })
      figures = this.flipY(figures)
      this.state = {
        figures, // mapping from label name to a list of Figure structures
        unfinishedFigure: null,
        figuresHistory: [],
        unfinishedFigureHistory: []
      }
    }

    flipY = figures => {
      console.log('flip y labeling app history hoc')
      // flip the y-coordinate
      const f = {}
      Object.keys(figures).forEach(label => {
        f[label] = figures[label].map(figure => {
          if (figure.label_type !== 'polygon' && figure.label_type !== 'bbox') return figure

          let tracingOptions
          console.log(tracingOptions)
          if (figure.tracingOptions && figure.tracingOptions.enabled) {
            tracingOptions = {
              ...figure.tracingOptions,
              trace: this.transformPoints(figure.tracingOptions.trace)
            }
          } else {
            tracingOptions = figure.tracingOptions
          }
          return {
            ...figure,
            points: this.transformPoints(figure.points),
            tracingOptions
          }
        })
      })
      return f
    }

    transformPoints = points => {
      console.log('transform points')
      const { height } = this.props
      return points.map(({ lat, lng, id, labeldata_id }) => ({
        lat: height - lat,
        lng,
        id: id || genId(),
        labeldata_id
      }))
    }

    componentDidUpdate(prevProps, prevState) {
      console.log('component did update')
      const { onLabelChange, height, width } = this.props
      const { figures } = this.state

      if (figures !== prevState.figures) {
        console.log('figures are not smae')
        onLabelChange({
          labels: this.flipY(figures),
          height,
          width
        })
      }
    }

    pushState = (stateChange, cb) => {
      console.log('push state')
      this.setState(
        state => ({
          figuresHistory: update(state.figuresHistory, {
            $push: [state.figures]
          }),
          unfinishedFigureHistory: update(state.unfinishedFigureHistory, {
            $push: [state.unfinishedFigure]
          }),
          ...stateChange(state)
        }),
        cb
      )
    }

    popState = () => {
      console.log('pop state')
      this.setState(state => {
        let { figuresHistory, unfinishedFigureHistory } = state
        if (!figuresHistory.length) {
          return {}
        }

        figuresHistory = figuresHistory.slice()
        unfinishedFigureHistory = unfinishedFigureHistory.slice()
        const figures = figuresHistory.pop()
        let unfinishedFigure = unfinishedFigureHistory.pop()

        if (unfinishedFigure && !unfinishedFigure.points.length) {
          unfinishedFigure = null
        }

        return {
          figures,
          unfinishedFigure,
          figuresHistory,
          unfinishedFigureHistory
        }
      })
    }

    render() {
      console.log('render labelling app history hoc')
      const { props, state, pushState, popState } = this
      const { figures, unfinishedFigure } = state
      const passedProps = {
        pushState,
        popState,
        figures,
        unfinishedFigure
      }
      return <Comp {...passedProps} {...props} />
    }
  }
}
