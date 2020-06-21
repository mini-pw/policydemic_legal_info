
import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Checkbox from '@material-ui/core/Checkbox';
import Paper from '@material-ui/core/Paper';

export default class SearchTableComponent extends React.Component {

    static headCells = [
        { id: 'source', numeric: false, disablePadding: true, label: 'Source' },
        { id: 'infoDate', numeric: true, disablePadding: false, label: 'Info date' },
        { id: 'language', numeric: true, disablePadding: false, label: 'Language' },
        { id: 'keywords', numeric: true, disablePadding: false, label: 'Keywords' },
        { id: 'country', numeric: true, disablePadding: false, label: 'Country' },
    ];

    createDataForRow(source, infoDate, language, keywords, country) {
        return {
            source: source,
            infoDate: infoDate,
            language: language,
            keywords: keywords,
            country: country
        };
    }

    render() {

        return (
            <Paper>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell padding="checkbox">

                                <Checkbox />

                            </TableCell>

                            {SearchTableComponent.headCells.map((headCell) => (
                                <TableCell
                                    key={headCell.id}
                                    align={headCell.numeric ? 'right' : 'left'}
                                    padding={headCell.disablePadding ? 'none' : 'default'}
                                >
                                </TableCell>
                            ))}

                        </TableRow>
                    </TableHead>

                    <TableBody>


                    </TableBody>
                </Table>

            </TableContainer>
            </Paper> 
        );
    }
}