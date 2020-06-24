
import React from 'react';
import Typography from '@material-ui/core/Typography';

export default class CrawlerConfigTabComponent extends React.Component {
    render() {
        return (<div>
            <Typography variant="h3">
                Crawler
            </Typography>
            <Typography variant="h4">
                Schedule
            </Typography>
            <Typography variant="h4">
                Search criteria
            </Typography>
        </div>)
    }
}