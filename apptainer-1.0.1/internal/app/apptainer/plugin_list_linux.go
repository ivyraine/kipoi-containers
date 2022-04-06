// Copyright (c) Contributors to the Apptainer project, established as
//   Apptainer a Series of LF Projects LLC.
//   For website terms of use, trademark policy, privacy policy and other
//   project policies see https://lfprojects.org/policies
// Copyright (c) 2018-2019, Sylabs Inc. All rights reserved.
// This software is licensed under a 3-clause BSD license. Please consult the
// LICENSE.md file distributed with the sources of this project regarding your
// rights to use or distribute this software.

package apptainer

import (
	"fmt"
	"sort"

	"github.com/apptainer/apptainer/internal/pkg/plugin"
)

// ListPlugins lists the apptainer plugins installed in the plugin
// plugin installation directory.
func ListPlugins() error {
	plugins, err := plugin.List()
	if err != nil {
		return err
	}

	if len(plugins) == 0 {
		fmt.Println("There are no plugins installed.")
		return nil
	}

	sort.Slice(plugins, func(i, j int) bool {
		return plugins[i].Name < plugins[j].Name
	})

	fmt.Printf("ENABLED  NAME\n")

	for _, p := range plugins {
		enabled := "no"
		if p.Enabled {
			enabled = "yes"
		}
		fmt.Printf("%7s  %s\n", enabled, p.Name)
	}

	return nil
}
