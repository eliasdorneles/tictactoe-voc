import org.gradle.api.Plugin
import org.gradle.api.Project


class VocPlugin implements Plugin<Project> {
    void apply(Project project) {
        project.extensions.create("voc", VocPluginExtension)

        project.task('vocBuild') {
            doLast {
                if (project.voc.buildFromSourceDir) {
                    def jarPath = "${project.voc.buildFromSourceDir}/dist/android/libs/python-android-support.jar"
                    project.exec {
                        workingDir "${project.voc.buildFromSourceDir}"
                        commandLine 'ant android'.split()
                    }
                    project.exec {
                        commandLine "cp ${jarPath} libs/".split()
                    }
                } else {
                    // TODO: download python-android-support.jar from an official release
                    throw new RuntimeException("Using an official release isn't implemented yet," +
                                               " please set voc.buildFromSourceDir to a local copy of VOC sources")
                }
                project.exec {
                    // TODO: compile a directory instead of a hardcoded module
                    commandLine "voc -v app.py -o libs -n ${project.voc.namespace}".split()
                }
                project.exec {
                    workingDir 'libs'
                    commandLine "jar cvf python-app.jar ${project.voc.namespace.replace('.', '/')}".split()
                }
            }
        }

        project.task('runAndroidVocApp') {
            doLast {
                project.exec {
                    commandLine "adb shell am start -n ${project.voc.namespace}/android.PythonActivity".split()
                }
            }
        }
    }
}


class VocPluginExtension {
    String namespace = "com.example"
    def buildFromSourceDir
}
