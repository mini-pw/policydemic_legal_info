import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import {
  KeyboardTimePicker,
  KeyboardDatePicker,
  DatePicker,
  MuiPickersUtilsProvider,
} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import {
  Container,
  Grid,
  Select,
  MenuItem,
  InputLabel,
  Switch,
  TextField,
  Button,
} from "@material-ui/core";
import SendIcon from "@material-ui/icons/Send";
import Api from "../../common/api";

const useStyles = makeStyles((theme) => ({
  select: {
    width: "100%",
    textAlign: "left",
  },
  label: {
    textAlign: "left",
  },
  section: {
    margin: "30px 0 20px 30px",
  },
}));

export default function CrawlerConfigTabComponent() {
  const classes = useStyles();
  const daysOfWeek = [
    "Monday",
    "Tuesday",
    "Wenesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];
  const today = new Date();
  const [isActive, setIsActive] = useState(true);
  const [minutes, setMinutes] = useState(today);
  const [hour, setHour] = useState(today);
  const [day, setDay] = useState(today);
  const [month, setMonth] = useState(today);
  const [dayOfWeek, setDayOfWeek] = useState(daysOfWeek[0]);
  const [searchPhrases, setSearchPhrases] = useState("");
  const [infoDateTo, setInfoDateTo] = useState(today);
  const [infoDateFrom, setInfoDateFrom] = useState(today);
  const [regex, setRegex] = useState("*.gov");

  const prepareState = () => {
    return {
      isActive,
      minutes: minutes.getMinutes(),
      hour: hour.getHours(),
      day: day.getDate(),
      month: month.getMonth(),
      dayOfWeek,
      searchPhrases: searchPhrases.split("\n"),
      infoDateFrom: infoDateFrom.toDateString(),
      infoDateTo: infoDateTo.toDateString(),
      regex,
    };
  };
  const saveConfig = () => {
    const config = prepareState();

    Api.saveCrawlerConfig(config).catch(() =>
      console.log("error encountered while saving crawler config")
    );
  };

  const runCrawler = () => {
    const config = prepareState();

    Api.runCrawler(config).catch(() =>
      console.log("error encountered while running crawler")
    );
  };

  return (
    <Container>
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <Grid container direction="column">
          {/* Crawler section  */}
          <Grid item>
            <Typography className={classes.label} variant="h5">
              Crawler
            </Typography>
          </Grid>
          <Grid
            container
            direction="column"
            alignItems="flex-start"
            className={classes.section}
            spacing={4}
          >
            <Grid item>
              <InputLabel className={classes.label} shrink>
                Is active
              </InputLabel>
              <Switch
                checked={isActive}
                onChange={(e) => setIsActive(e.target.checked)}
              />
            </Grid>
          </Grid>
          {/* Schedule section */}
          <Grid item>
            <Typography className={classes.label} variant="h5">
              Schedule
            </Typography>
          </Grid>
          <Grid
            container
            justify="space-between"
            spacing={4}
            className={classes.section}
          >
            <Grid item xs={2}>
              <KeyboardTimePicker
                ampm={false}
                views={["minutes"]}
                label="Minutes"
                value={minutes}
                onChange={setMinutes}
                format="mm"
              />
            </Grid>
            <Grid item xs={2}>
              <KeyboardTimePicker
                disableToolbar
                ampm={false}
                views={["hours"]}
                label="Hour"
                value={hour}
                onChange={setHour}
                format="HH"
              />
            </Grid>
            <Grid item xs={2}>
              <KeyboardDatePicker
                disableToolbar
                views={["date"]}
                label="Day of month"
                value={day}
                onChange={setDay}
                format="dd"
              />
            </Grid>
            <Grid item xs={3}>
              <DatePicker
                disableToolbar
                views={["month"]}
                label="Month"
                value={month}
                onChange={setMonth}
                format="MMMM"
              />
            </Grid>
            <Grid item xs={3}>
              <InputLabel
                shrink
                className={classes.label}
                id="day-of-week-select-label"
              >
                Day of week
              </InputLabel>
              <Select
                className={classes.select}
                value={dayOfWeek}
                labelId="day-of-week-select-label"
                id="day-of-week-select"
                onChange={(e) => setDayOfWeek(e.target.value)}
              >
                {daysOfWeek.map((day) => (
                  <MenuItem value={day} key={day}>
                    {day}
                  </MenuItem>
                ))}
              </Select>
            </Grid>
          </Grid>
          {/* Section search criteria */}
          <Grid item>
            <Typography className={classes.label} variant="h5">
              Search criteria
            </Typography>
          </Grid>
          <Grid
            container
            justify="space-between"
            spacing={4}
            className={classes.section}
          >
            <Grid item xs={6}>
              <TextField
                multiline
                value={searchPhrases}
                onChange={(e) => setSearchPhrases(e.target.value)}
                variant="outlined"
                label="Search phrases, new line separated"
                placeholder="Enter search phrases"
                fullWidth
              />
            </Grid>
            <Grid item xs={2}>
              <DatePicker
                label="Info date from"
                value={infoDateFrom}
                onChange={setInfoDateFrom}
                format="dd/MM/yyyy"
              />
            </Grid>

            <Grid item xs={2}>
              <DatePicker
                label="Info date to"
                value={infoDateTo}
                onChange={setInfoDateTo}
                format="dd/MM/yyyy"
              />
            </Grid>
            <Grid item xs={2}>
              <TextField
                value={regex}
                onChange={(e) => setRegex(e.target.value)}
                label="Website regex"
                placeholder="Enter website regex"
              />
            </Grid>
          </Grid>
          <Grid container justify="flex-end" spacing={4}>
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                endIcon={<SendIcon />}
                onClick={runCrawler}
              >
                Run now
              </Button>
            </Grid>
            <Grid item>
              <Button variant="contained" color="primary" onClick={saveConfig}>
                Save
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </MuiPickersUtilsProvider>
    </Container>
  );
}
