// Copyright (c) Contributors to the Apptainer project, established as
//   Apptainer a Series of LF Projects LLC.
//   For website terms of use, trademark policy, privacy policy and other
//   project policies see https://lfprojects.org/policies
// Copyright (c) 2020, Sylabs Inc. All rights reserved.
// This software is licensed under a 3-clause BSD license. Please consult the
// LICENSE.md file distributed with the URIs of this project regarding your
// rights to use or distribute this software.

package main

import (
	"os"
	"strconv"

	"github.com/apptainer/apptainer/pkg/cmdline"
	pluginapi "github.com/apptainer/apptainer/pkg/plugin"
	clicallback "github.com/apptainer/apptainer/pkg/plugin/callback/cli"
	"github.com/apptainer/apptainer/pkg/runtime/engine/config"
	"github.com/spf13/cobra"
)

// Plugin is the only variable which a plugin MUST export.
// This symbol is accessed by the plugin framework to initialize the plugin.
var Plugin = pluginapi.Plugin{
	Manifest: pluginapi.Manifest{
		Name:        "github.com/apptainer/apptainer/e2e-cli-plugin",
		Author:      "Sylabs Team",
		Version:     "0.1.0",
		Description: "E2E CLI plugin",
	},
	Callbacks: []pluginapi.Callback{
		(clicallback.Command)(callbackExitCmd),
		(clicallback.ApptainerEngineConfig)(callbackApptainer),
	},
}

func callbackExitCmd(manager *cmdline.CommandManager) {
	manager.RegisterCmd(&cobra.Command{
		DisableFlagsInUseLine: true,
		Args:                  cobra.ExactArgs(1),
		Use:                   "exit <code>",
		Short:                 "Exit with code",
		Long:                  "Exit with code",
		Example:               "apptainer exit 42",
		Run: func(cmd *cobra.Command, args []string) {
			code, err := strconv.Atoi(args[0])
			if err != nil {
				os.Exit(255)
			}
			os.Exit(code)
		},
		TraverseChildren: true,
	})
}

func callbackApptainer(_ *config.Common) {
	os.Exit(43)
}
