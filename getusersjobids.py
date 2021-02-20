import click
import rich
from tabulate import tabulate
import subprocess


class dataFactory:
    """Class to write out jobs ids into specific formats requested by user."""
    def __init__(self, data):
        self.data = data

    def toXML(self):
        """Function to write data in XML format."""
        pass

    def toJSON(self):
        """Function to write data in JSON format."""
        pass

    def toYAML(self):
        """Function to write data in YAML format."""
        pass

    def toCSV(self):
        """Function to write data in CSV format."""
        pass

    def toTABLE(self):
        """Function to write data in TABLE format."""
        pass


def retrieveIDS(user_id, days, output_file):
    """Function to search through job logs on torque."""
    # Retreive past couple of job log directories
    job_log_dir = "/var/spool/torque/job_logs"
    job_logs = subprocess.Popen(["ls", job_log_dir, "-t"], stdout=subprocess.PIPE)
    logs = subprocess.run(["head", "-n", days], stdin=job_logs.stdout, capture_output=True, text=True)
    job_logs.stdout.close()

    # Convert logs.stdout to a list and remove any blank lines
    logs_list = logs.stdout.split("\n")
    logs_list.remove("")

    # Loop through each job log to find job ids
    for log in logs_list:
        # Command chain to extract job ids
        command_1 = subprocess.Popen(["cat", "{}/{}".format(job_log_dir, log)], stdout=subprocess.PIPE)
        command_2 = subprocess.Popen(["grep", "-n", "<Job_Owner>{}".format(user_id)], stdin=command_1.stdout, stdout=subprocess.PIPE)
        command_3 = subprocess.run(["cut", "-d:", "-f1"], stdin=command_2.stdout, capture_output=True, text=True)
        command_1.stdout.close()
        command_2.stdout.close()

        # Convert command_3 to line_numbers list and remove any blank lines
        line_numbers = command_3.stdout.split("\n")
        line_numbers.remove("")

        # Loop through line number and retrieve XML tag
        for line_number in line_numbers:
            line_number = subprocess.run(["expr", line_number, "-", "2"], capture_output=True, text=True)
            command_4 = subprocess.Popen(["head", "-n", line_number.stdout.strip("\n"), "{}/{}".format(job_log_dir, log)], stdout=subprocess.PIPE)
            final_output = subprocess.run(["tail", "-n", "1"], stdin=command_4.stdout, capture_output=True, text=True)
            command_4.stdout.close()
            print(final_output.stdout.strip("\n"))


@click.command()
@click.argument("user", nargs=-1)
@click.option("-d", "--days", default=5, help="Specify the number of days to check in the torque job logs (default: 5)")
@click.option("--xml", is_flag=True, help="Print job ids in XML format")
@click.option("--json", is_flag=True, help="Print job ids in JSON format")
@click.option("--yaml", is_flag=True, help="Print job ids in YAML format")
@click.option("--csv", is_flag=True, help="Print job ids in CSV format")
@click.option("--table", is_flag=True, help="Print job ids in tabular format")
@click.option("-V", "--version", is_flag=True, help="Print version info.")
@click.option("--license", is_flag=True, help="Print licensing info.")
def main(user, days, xml, json, yaml, csv, table, version, license):
    if version:
        click.echo("getusersjobids v2.0  Copyright (C) 2021  Jason C. Nucciarone \n\n"
                   "This program comes with ABSOLUTELY NO WARRANTY; \n"
                   "for more details type \"getusersjobids --license\". This is free software, \n"
                   "and you are welcome to redistribute it under certain conditions; \n"
                   "go to https://www.gnu.org/licenses/licenses.html for more details.")
        exit()

    elif license:
        click.echo("""getusersjobids: Retrieve users job ids for processing and analization.\n
    Copyright (C) 2021  Jason C. Nucciarone

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.""")
        exit()

    else:
        pass


if __name__ == "__main__":
    main()
