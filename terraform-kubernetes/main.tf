resource "kubernetes_manifest" "deployment_terraform_monitoring" {
  manifest = {
    "apiVersion" = "apps/v1"
    "kind" = "Deployment"
    "metadata" = {
      "annotations" = {
        "prometheus.io/path" = "/metrics"
        "prometheus.io/port" = "roboport"
        "prometheus.io/scrape" = "true"
      }
      "labels" = {
        "name" = "terraform-monitoring"
        "release" = "prometheus"
      }
      "name" = "terraform-monitoring"
      "namespace" = "default"
    }
    "spec" = {
      "replicas" = 1
      "selector" = {
        "matchLabels" = {
          "app" = "terraform-monitoring"
        }
      }
      "template" = {
        "metadata" = {
          "labels" = {
            "app" = "terraform-monitoring"
          }
        }
        "spec" = {
          "containers" = [
            {
              "image" = "linuxrobotgeek/terraform-monitoring:latest"
              "imagePullPolicy" = "Always"
              "name" = "terraform-monitoring"
              "ports" = [
                {
                  "containerPort" = 5000
                  "name" = "roboport"
                  "protocol" = "TCP"
                },
              ]
            },
          ]
        }
      }
    }
  }
}

resource "kubernetes_manifest" "service_terraform_monitoring" {
  manifest = {
    "apiVersion" = "v1"
    "kind" = "Service"
    "metadata" = {
      "labels" = {
        "app" = "terraform-monitoring"
      }
      "name" = "terraform-monitoring"
      "namespace" = "default"
    }
    "spec" = {
      "ports" = [
        {
          "name" = "terraform-monitoring"
          "port" = 5000
          "protocol" = "TCP"
          "targetPort" = "roboport"
        },
      ]
      "selector" = {
        "app" = "terraform-monitoring"
      }
      "type" = "LoadBalancer"
    }
  }
}

resource "kubernetes_manifest" "servicemonitor_monitoring_terraform_monitoring" {
  manifest = {
    "apiVersion" = "monitoring.coreos.com/v1"
    "kind" = "ServiceMonitor"
    "metadata" = {
      "labels" = {
        "app" = "terraform-monitoring"
        "release" = "prometheus"
      }
      "name" = "terraform-monitoring"
      "namespace" = "monitoring"
    }
    "spec" = {
      "endpoints" = [
        {
          "interval" = "15s"
          "path" = "/metrics"
          "port" = "terraform-monitoring"
        },
      ]
      "namespaceSelector" = {
        "matchNames" = [
          "default",
        ]
      }
      "selector" = {
        "matchLabels" = {
          "app" = "terraform-monitoring"
        }
      }
    }
  }
}
